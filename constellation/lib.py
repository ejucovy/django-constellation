
import os
import sys
import time
import locale
import urlparse

from ConfigParser import ConfigParser

import planet

def config_get(config, section, option, default=None, raw=0, vars=None):
    """Get a value from the configuration, with a default."""
    if config.has_option(section, option):
        return config.get(section, option, raw=raw, vars=None)
    else:
        return default

def run_planet(config_file=None, 
               PLANET_NAME="Unconfigured Planet", 
               PLANET_LINK="Unconfigured Planet",
               PLANET_FEED=None,
               OWNER_NAME="Anonymous Coward", 
               OWNER_EMAIL="",
               verbose=0,
               offline=0,
               LOG_LEVEL="WARNING",
               FEED_TIMEOUT=20,
               TEMPLATE_FILES="examples/basic/planet.html.tmpl"):
    # Read the configuration file
    config = ConfigParser()
    config.read(config_file)
    assert config.has_section("Planet"), \
        "Configuration missing [Planet] section."

    # Read the [Planet] config section
    planet_name = config_get(config, "Planet", "name",        PLANET_NAME)
    planet_link = config_get(config, "Planet", "link",        PLANET_LINK)
    planet_feed = config_get(config, "Planet", "feed",        PLANET_FEED)
    owner_name  = config_get(config, "Planet", "owner_name",  OWNER_NAME)
    owner_email = config_get(config, "Planet", "owner_email", OWNER_EMAIL)

    if verbose:
        log_level = "DEBUG"
    else:
        log_level  = config_get(config, "Planet", "log_level", LOG_LEVEL)
    feed_timeout   = config_get(config, "Planet", "feed_timeout", FEED_TIMEOUT)
    template_files = config_get(config, "Planet", "template_files",
                                TEMPLATE_FILES).split(" ")

    # Default feed to the first feed for which there is a template
    if not planet_feed:
        for template_file in template_files:
            name = os.path.splitext(os.path.basename(template_file))[0]
            if name.find('atom')>=0 or name.find('rss')>=0:
                planet_feed = urlparse.urljoin(planet_link, name)
                break

    # Define locale
    if config.has_option("Planet", "locale"):
        # The user can specify more than one locale (separated by ":") as
        # fallbacks.
        locale_ok = False
        for user_locale in config.get("Planet", "locale").split(':'):
            user_locale = user_locale.strip()
            try:
                locale.setlocale(locale.LC_ALL, user_locale)
            except locale.Error:
                pass
            else:
                locale_ok = True
                break
        if not locale_ok:
            print >>sys.stderr, "Unsupported locale setting."
            sys.exit(1)

    # Activate logging
    planet.logging.basicConfig()
    planet.logging.getLogger().setLevel(planet.logging.getLevelName(log_level))
    log = planet.logging.getLogger("planet.runner")
    try:
        log.warning
    except:
        log.warning = log.warn

    # timeoutsocket allows feedparser to time out rather than hang forever on
    # ultra-slow servers.  Python 2.3 now has this functionality available in
    # the standard socket library, so under 2.3 you don't need to install
    # anything.  But you probably should anyway, because the socket module is
    # buggy and timeoutsocket is better.
    if feed_timeout:
        try:
            feed_timeout = float(feed_timeout)
        except:
            log.warning("Feed timeout set to invalid value '%s', skipping", feed_timeout)
            feed_timeout = None

    if feed_timeout and not offline:
        try:
            from planet import timeoutsocket
            timeoutsocket.setDefaultSocketTimeout(feed_timeout)
            log.debug("Socket timeout set to %d seconds", feed_timeout)
        except ImportError:
            import socket
            if hasattr(socket, 'setdefaulttimeout'):
                log.debug("timeoutsocket not found, using python function")
                socket.setdefaulttimeout(feed_timeout)
                log.debug("Socket timeout set to %d seconds", feed_timeout)
            else:
                log.error("Unable to set timeout to %d seconds", feed_timeout)

    # run the planet
    my_planet = planet.Planet(config)
    my_planet.run(planet_name, planet_link, template_files, offline)

    my_planet.generate_all_files(template_files, planet_name,
        planet_link, planet_feed, owner_name, owner_email)
