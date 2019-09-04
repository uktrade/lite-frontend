def convert_dict_to_query_params(dictionary):
    return '&'.join(([key + '=' + str(value) for (key, value) in dictionary.items()]))
