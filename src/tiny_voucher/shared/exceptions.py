class DomainExceptionError(Exception):
    pass


class VoucherUseCaseExceptionError(DomainExceptionError):
    pass


class VoucherServiceExceptionError(VoucherUseCaseExceptionError):
    pass


class InstanceNotFoundExceptionError(Exception):
    pass
