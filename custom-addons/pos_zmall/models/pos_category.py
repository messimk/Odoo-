from odoo import fields, models
from odoo import api, fields, models, _
import json, requests
import logging
import uuid
import random
import string
import base64
from odoo.exceptions import UserError

from odoo.http import Response, request

_logger = logging.getLogger(__name__)
# _logger.setLevel(logging.WARNING)



class PosCategory(models.Model):
    _inherit = "pos.category"
    zmall_category_id = fields.Char(string='Zmall Category ID')