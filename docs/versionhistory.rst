Version history
===============

This library adheres to `Semantic Versioning <http://semver.org/>`_.

**UNRELEASED**

- Dropped support for Python 3.7
- Dropped support for Asphalt earlier than 4.8
- Dropped support for motor earlier than 3.3
- Dropped support for the Asphalt context variable

**3.0.1** (2017-06-04)

- Added compatibility with Asphalt 4.0
- Added Docker configuration for easier local testing

**3.0.0** (2017-04-10)

- **BACKWARD INCOMPATIBLE** Migrated to Asphalt 3.0

**2.0.0** (2016-11-05)

- **BACKWARD INCOMPATIBLE** Upgraded to  Motor 1.0
- **BACKWARD INCOMPATIBLE** The ``address`` option has been replaced with ``host``,
  which is now directly passed to ``AsyncIOMotorEngine``

**1.0.0** (2016-10-04)

- Initial release
