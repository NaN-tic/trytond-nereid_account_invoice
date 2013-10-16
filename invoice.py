#This file is part nereid_account_invoice module for Tryton.
#The COPYRIGHT file at the top level of this repository contains 
#the full copyright notices and license terms.
from nereid import render_template, request, login_required
from nereid.helpers import url_for
from nereid.contrib.pagination import Pagination
from werkzeug.exceptions import NotFound

from trytond.pool import PoolMeta

__all__ = ['Invoice']
__metaclass__ = PoolMeta

_TYPE = ['out_invoice', 'out_credit_note']


class Invoice:
    __name__ = 'account.invoice'

    per_page = 10

    @classmethod
    @login_required
    def render_list(cls):
        """
        Get invoices
        """
        page = request.args.get('page', 1, int)

        clause = []
        clause.append(('party', '=', request.nereid_user.party))
        clause.append(('type', 'in', _TYPE))
        order = [('invoice_date', 'DESC'), ('id', 'DESC')]

        invoices = Pagination(
            cls, clause, page, cls.per_page, order
        )

        return render_template('invoices.jinja', invoices=invoices)

    @classmethod
    @login_required
    def render(cls, uri):
        """
        Get invoice detail
        """
        try:
            invoice, = cls.search([
                ('id', '=', int(uri)),
                ('party', '=', request.nereid_user.party),
                ])
        except ValueError:
            return NotFound()
        return render_template('invoice.jinja', invoice=invoice)

    def get_absolute_url(self, **kwargs):
        return url_for(
            'account.invoice.render', uri=self.id, **kwargs
            )
