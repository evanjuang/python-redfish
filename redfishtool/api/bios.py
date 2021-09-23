from redfishtool.utils.misc import DictUtil


def get_attr_type(reg_attr):
    _type = reg_attr.get('Type')
    if _type == 'Enumeration':
        return {
            'type': 'enum',
            'allowable': [_.get('ValueName') for _ in reg_attr.get('Value')]
        }
    elif _type == 'String':
        return {
            'type': 'str',
            'min_len': reg_attr.get('MinLength'),
            'max_len': reg_attr.get('MaxLength')
        }
    elif _type == 'Integer':
        return {
            'type': 'int',
            'upper': reg_attr.get('UpperBound'),
            'lower': reg_attr.get('LowerBound'),
            'step': reg_attr.get('ScalarIncrement')
        }


def keyword_filter(reg_attr, keyword):
    if (keyword in reg_attr.get('DisplayName') or keyword in reg_attr.get('HelpText')):
        return True
    return False


def get_bios_service(rf_conn):
    rf_root = rf_conn.service_root
    return rf_root.get_system().get_bios()


def _get_bios_current_setting(rf_bios):
    return rf_bios.attribute


def _get_bios_hii(rf_bios):
    reg_resource = rf_bios.get_attribute_registry()
    return DictUtil.get(reg_resource.data, 'RegistryEntries', 'Attributes')


def _get_bios_setting_with_hii(rf_bios, filter_args=None, filter=keyword_filter, verbose=False):
    cur_setting = _get_bios_current_setting(rf_bios)
    hii_attrs = _get_bios_hii(rf_bios)

    bios_hii = []
    if hii_attrs:
        for _ in hii_attrs:
            if filter_args and not (filter)(_, filter_args):
                continue

            attr_name = _.get('AttributeName')
            attr = {
                'name': _.get('DisplayName'),
                'attr_name': attr_name,
                'value': cur_setting.get(attr_name),
                'value_type': get_attr_type(_)
            }

            if verbose:
                attr['help'] = _.get('HelpText')
                attr['read_only'] = _.get('ReadOnly')

            bios_hii.append(attr)

    return bios_hii


def _valid_setting_value(cur, new):
    val_type = cur.get('value_type')

    if val_type.get('type') == 'str':
        return isinstance(new, str) and (len(new) <= val_type.get('max_len')) and (len(new) >= val_type.get('min_len'))

    if val_type.get('type') == 'int':
        return isinstance(new, int) and (new <= val_type.get('upper')) and (new >= val_type.get('lower'))

    if val_type.get('type') == 'enum':
        return (isinstance(new, str) or isinstance(new, int)) and new in val_type.get('allowable')


def _find_bios_attr(cur_bios, name):
    for attr in cur_bios:
        if attr.get('attr_name') == name:
            return attr
    return None


def get_bios_setting(rf_conn, hii=False, filter_args=None, filter=keyword_filter, verbose=False):
    rf_bios = get_bios_service(rf_conn)
    if not hii:
        return _get_bios_current_setting(rf_bios)

    else:
        return _get_bios_setting_with_hii(rf_bios, filter_args=filter_args, filter=keyword_filter, verbose=verbose)


def update_bios_setting(rf_conn, settings):
    invalid = []
    valid = {}

    if not isinstance(settings, dict):
        raise TypeError()

    rf_bios = get_bios_service(rf_conn)
    cur_bios = _get_bios_setting_with_hii(rf_bios, verbose=True)

    cur_attr = None
    for k, v in settings.items():
        cur_attr = _find_bios_attr(cur_bios, k)
        if not cur_attr:
            invalid.append((k, v, 'attribute not found'))
            continue

        if cur_attr.get('read_only') is True:
            invalid.append((k, v, 'attribute is readonly'))
            continue

        if not _valid_setting_value(cur_attr, v):
            invalid.append((k, v, 'invalid value'))
            continue

        if v == cur_attr.get('value'):
            invalid.append((k, v, 'same value'))
            continue

        valid.update({k: v})

    if not invalid and valid:
        print(valid)
        print(invalid)
        bios_setting = rf_bios.get_settings_object()
        bios_setting.update(valid)

    else:
        raise ValueError(str(invalid))


def get_bios_pending_setting(rf_conn):
    rf_bios = get_bios_service(rf_conn)
    rf_bios_setting = rf_bios.get_settings_object()

    return rf_bios_setting.attribute if rf_bios_setting else {}


def undo_bios_pending_setting(rf_conn):
    rf_bios = get_bios_service(rf_conn)
    rf_bios_setting = rf_bios.get_settings_object()

    cur = _get_bios_current_setting(rf_bios)
    new = rf_bios_setting.attribute

    if new:
        undo = {k: cur.get(k) for k in new.keys()}
        rf_bios_setting.update(undo)
