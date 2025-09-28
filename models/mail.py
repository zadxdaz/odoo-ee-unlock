# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import datetime
import logging
from ast import literal_eval

import requests

from odoo import api, fields, release, SUPERUSER_ID
from odoo.exceptions import UserError
from odoo.models import AbstractModel
from odoo.tools.translate import _
from odoo.tools import config
import random
import string

_logger = logging.getLogger(__name__)


class PublisherWarrantyContract(AbstractModel):
    _name = "publisher_warranty.contract"
    _description = 'Publisher Warranty Contract'

    def update_notification(self, cron_mode=True):
        """
        Send a message to Odoo's publisher warranty server to check the
        validity of the contracts, get notifications, etc...

        @param cron_mode: If true, catch all exceptions (appropriate for usage in a cron).
        @type cron_mode: boolean
        """
        try:
            user = self.env['res.users'].sudo().browse(SUPERUSER_ID)
            poster = self.sudo().env.ref('mail.channel_all_employees')
            set_param = self.env['ir.config_parameter'].sudo().set_param
            expiration_date = (datetime.datetime.now() + datetime.timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')
            set_param('database.expiration_date', expiration_date)
            set_param('database.expiration_reason', "renewal")
            def generate_random_code():
                letter = random.choice(string.ascii_uppercase)
                numbers = ''.join(random.choices(string.digits, k=14))
                return letter + numbers

            set_param('database.enterprise_code', generate_random_code())
            set_param('database.already_linked_subscription_url', "")
            set_param('database.already_linked_email', "")
            set_param('database.already_linked_send_mail_url', "")

        except Exception:
            if cron_mode:
                return False    # we don't want to see any stack trace in cron
            else:
                raise
        return True
