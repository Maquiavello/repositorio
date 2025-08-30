class AppRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'mi_app':
            return 'default'  # ¡Ahora usa PostgreSQL!
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'mi_app':
            return 'default'  # ¡Ahora usa PostgreSQL!
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'mi_app':
            return db == 'default'  # ¡Ahora usa PostgreSQL!
        return None