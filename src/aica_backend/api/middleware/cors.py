class CORSConfig:
    def get_config(self):
        return {
            "allow_origins": self._get_allowed_origins(),
            "allow_credentials": True,
            "allow_methods": self._get_allowed_methods(),
            "expose_headers": self._get_exposed_headers(),
            "max_age": 86400,
        }
