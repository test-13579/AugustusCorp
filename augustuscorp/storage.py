from whitenoise.storage import CompressedManifestStaticFilesStorage


class WhiteNoiseStorage(CompressedManifestStaticFilesStorage):
    # Don't raise errors for CSS url() references that can't be resolved
    # (e.g. Django admin SVGs referenced from admin CSS).
    manifest_strict = False
