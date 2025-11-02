class DomainExceptionError(Exception):
    pass


class ValueObjectExceptionError(Exception):
    pass


class VoucherUseCaseExceptionError(DomainExceptionError):
    pass


class VoucherServiceExceptionError(VoucherUseCaseExceptionError):
    pass


class CampaignServiceExceptionError(VoucherUseCaseExceptionError):
    pass


class InstanceExistsExceptionError(DomainExceptionError):
    pass


class InstanceNotFoundExceptionError(DomainExceptionError):
    pass
