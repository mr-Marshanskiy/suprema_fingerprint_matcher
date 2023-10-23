import base64
from .imports import ufm_lib
from ctypes import *

from fingerprints.tools.matcher.error import MatcherError


MAX_TEMPLATE_SIZE = 1024

TEMPLATE_TYPES = {
    2001: 'Suprema template type',
    2002: 'ISO template type',
    2003: 'ANSI378 template type',
}


class FingerMatcher:
    timeout = 20
    h_matcher = None
    template_type = None
    matcher_params = {
        302: 1,
    }

    def __init__(self, template_type=2002, matcher_params=None):
        assert template_type in TEMPLATE_TYPES.keys(), (
            f'Specify one of the template types: '
            f'{", ".join(f"{key} - {value}" for key, value in TEMPLATE_TYPES.items())}'
        )
        self.template_type = template_type
        self.matcher_params = matcher_params or self.matcher_params
        self.h_matcher = self._get_matcher()
        self._set_matcher_template()
        self._set_matcher_params()

    def _get_matcher(self):
        h_matcher = c_void_p()
        ufm_res = ufm_lib.UFM_Create(byref(h_matcher))
        if ufm_res != 0:
            raise MatcherError('Matcher creating failed')
        return h_matcher

    def _set_matcher_template(self):
        nTemplateType = c_int(self.template_type)
        ufm_res = ufm_lib.UFM_SetTemplateType(self.h_matcher, nTemplateType)
        if ufm_res != 0:
            raise MatcherError('Error setting template type.')
        return

    def _set_matcher_params(self):

        for code, value in self.matcher_params.items():
            ufm_res = ufm_lib.UFM_SetParameter(
                self.h_matcher,
                c_int(code),
                byref(c_int(value)),
            )
            if ufm_res != 0:
                raise MatcherError('Error setting parameters.')
        return

    def identify(self, target_template, templates):
        len_templates = len(templates)
        target_template = self.beautify_template(target_template)
        target_template_size = sizeof(c_ubyte * MAX_TEMPLATE_SIZE)
        tmp_array, tmp_size_array = self.beautify_template_array(templates)

        templates_count = c_int(len_templates)
        proc_timeout = c_int(self.timeout)
        result_index = c_int()

        response = ufm_lib.UFM_Identify(
            self.h_matcher,
            target_template,
            target_template_size,
            tmp_array,
            tmp_size_array,
            templates_count,
            proc_timeout,
            byref(result_index)
        )
        return response, result_index

    def verify(self, target_template, template_in_db):
        target_template = self.beautify_template(target_template)
        template_in_db = self.beautify_template(template_in_db)
        target_template_size = sizeof(c_ubyte * MAX_TEMPLATE_SIZE)
        template_size_in_db = sizeof(c_ubyte * MAX_TEMPLATE_SIZE)
        result_index = c_int()

        response = ufm_lib.UFM_Verify(
            self.h_matcher,
            target_template,
            target_template_size,
            template_in_db,
            template_size_in_db,
            byref(result_index)
        )
        return response, result_index

    def beautify_template(self, template_str):
        template_bytes = base64.b64decode(template_str)
        data_ubyte = (c_ubyte * len(template_bytes))(*template_bytes)
        template = cast(data_ubyte, POINTER(c_ubyte))
        return template

    def beautify_template_array(self, templates_str):
        len_templates = len(templates_str)
        templates_array = (POINTER(c_ubyte) * len_templates)()
        templates_size_array = (c_long * len_templates)()

        for i, template in enumerate(templates_str):
            template = self.beautify_template(template)
            templates_array[i] = cast(template, POINTER(c_ubyte))
            templates_size_array[i] = sizeof(c_ubyte * MAX_TEMPLATE_SIZE)

        return templates_array, templates_size_array
