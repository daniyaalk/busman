class InvoicePermissionSetterMixin:

    def __init__(self):
        if self.__class__.__name__[:5] == 'Sales':
            self.permissions_required = ['sales_permissions']
        else:
            self.permissions_required = ['purchase_permissions']

        return super().__init__();