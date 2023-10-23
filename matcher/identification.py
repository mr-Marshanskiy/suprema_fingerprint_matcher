import base64
import os
from ctypes import *
import platform
from config.settings import BASE_DIR
from identification.tools.matcher.error import MatcherError

current_os = platform.system()

if current_os == 'Windows':
    ufm_lib = CDLL(
        os.path.join(
            BASE_DIR,
            'identification/tools/matcher/UFMatcher.dll'
        )
    )
else:
    CDLL('/lib/x86_64-linux-gnu/libusb-1.0.so', mode=RTLD_GLOBAL)
    ufm_lib = CDLL(
        os.path.join(
            BASE_DIR,
            'identification/tools/matcher/libUFMatcher.so'
        ), mode=RTLD_GLOBAL
    )


class FingerMatcher:
    h_matcher = None
    MAX_TEMPLATE_SIZE = 1024

    def __init__(self):
        self.h_matcher = self._get_matcher()
        self._set_matcher_params()

    def _get_matcher(self):
        h_matcher = c_void_p()
        ufm_res = ufm_lib.UFM_Create(byref(h_matcher))
        if ufm_res != 0:
            print(ufm_res)
            raise MatcherError('Matcher creating failed')
        nTemplateType = c_int(2002)
        ufs_res = ufm_lib.UFM_SetTemplateType(h_matcher, nTemplateType)
        if ufm_res != 0:
            print(ufm_res)
            raise MatcherError('Matcher set template type failed')
        return h_matcher

    def _set_matcher_params(self):
        param_code = c_int(302)
        param_value = c_int(1)
        response = ufm_lib.UFM_SetParameter(
            self.h_matcher,
            param_code,
            byref(param_value),
        )
        return response

    def identify(self, target_template, templates):
        len_templates = len(templates)
        target_template = self.beautify_template(target_template)
        target_template_size = sizeof(c_ubyte * self.MAX_TEMPLATE_SIZE)
        tmp_array, tmp_size_array = self.beautify_template_array(templates)

        templates_count = c_int(len_templates)
        proc_timeout = c_int(20)
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
        target_template_size = sizeof(c_ubyte * self.MAX_TEMPLATE_SIZE)
        template_size_in_db = sizeof(c_ubyte * self.MAX_TEMPLATE_SIZE)
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
            templates_size_array[i] = sizeof(c_ubyte * self.MAX_TEMPLATE_SIZE)

        return templates_array, templates_size_array
