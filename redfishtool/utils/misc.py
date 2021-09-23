import shutil


def cmd_exists(cmd):
    """Check if required commands is installed"""
    return shutil.which(cmd) is not None


class DictUtil():
    @staticmethod
    def get(dict_data, *keys):
        for key in keys:
            if isinstance(dict_data, dict):
                dict_data = dict_data.get(key, None)
            else:
                return None
        return dict_data

    @staticmethod
    def find(dict_data, key_list):
        if isinstance(key_list, list):
            for k in key_list:
                v = DictUtil.get(dict_data, *k)
                if v:
                    return v
        return None
