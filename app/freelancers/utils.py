class Currency():
    """
    ENUM for the currencies.
    """

    EURO = 'EUR'
    DOLLAR = 'USD'
    # TODO change strings to actual signs.
    CURRENCY_CHOICES = (
        (EURO, 'Euro'),
        (DOLLAR, 'Dollar'),
    )


def create_invoice_file_path(invoice):
    """
    Returns the file path to where an invoice pdf needs to be saved
    """

    file_path = '%(year)04d/%(month)02d/%(day)02d/%(id)d.pdf' % {'year': invoice.date_generated.year,
                                                                 'month': invoice.date_generated.month,
                                                                 'day': invoice.date_generated.day,
                                                                 'id': invoice.pk}

    return file_path
