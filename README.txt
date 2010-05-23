You must provide some Django settings:

PLANET_CONFIG_DIR: 
 Full path on filesystem to a directory where individual Planet
 configurations will be written and read.  These are temporary files
 which are written as needed based on values stored in the database.

 The directory must exist.

PLANET_OUTPUT_DIR:
 Full path on filesystem where Planet output should be written
 to. These are the publishable files that Planet generates, typically
 served by a static fileserver. Constellation treats these files as
 templates and serves them on particular views.

 This path should also be included in your Django TEMPLATE_DIRS settings.

 The directory must exist.

PLANET_CACHE_DIR:
 Full path on filesystem where Planet will store cached feeds. These
 can be wiped at any time.

 The directory must exist.

PLANET_TEMPLATE_FILES: (optional)
 Space-separated list of full paths on filesystem where templates for
 Planet output are stored.

 Constellation provides a default Planet template in its distribution;
 this will be the default if no setting is provided.
