from django.http import HttpResponseRedirect
from urllib.parse import urlencode, urlparse, urlunparse, parse_qsl


# def remember_last_query_params(url_name, query_params):
    """Stores the specified list of query params from the last time this user
    looked at this URL (by url_name). Stores the last values in the session.
    If the view is subsequently rendered w/o specifying ANY of the query params,
    it will redirect to the same URL with the last query params added to the URL.

    url_name is a unique identifier key for this view or view type if you want
    to group multiple views together in terms of shared history

    Example:

    @remember_last_query_params("jobs", ["category", "location"])
    def myview(request):
        pass

    """

    # def is_query_params_specified(request, query_params):
    #     """ Are any of the query parameters we are interested in on this request URL?"""
    #     for current_param in request.GET:
    #         if current_param in query_params:
    #             return True
    #     return False

    # def params_from_last_time(request, key_prefix, query_params):
    #     """ Gets a dictionary of JUST the params from the last render with values """
    #     params = {}
    #     for query_param in query_params:
    #         last_value = request.session.get(key_prefix + query_param)
    #         if last_value:
    #             params[query_param] = last_value
    #     return params

    # def update_url(url, params):
    #     """ update an existing URL with or without paramters to include new parameters
    #     from http://stackoverflow.com/questions/2506379/add-params-to-given-url-in-python
    #     """
    #     if not params:
    #         return url
    #     if not url:  # handle None
    #         url = ""
    #     url_parts = list(urlparse(url))
    #     # http://docs.python.org/library/urlparse.html#urlparse.urlparse, part 4 == params
    #     query = dict(parse_qsl(url_parts[4]))
    #     query.update(params)
    #     url_parts[4] = urlencode(query)
    #     return urlunparse(url_parts)

    # def do_decorator(view_func):

    #     def decorator(*args, **kwargs):

    #         request = args[0]

    #         key_prefix = url_name + "_"

    #         if is_query_params_specified(request, query_params):
    #             for query_param in query_params:
    #                 request.session[key_prefix +
    #                                 query_param] = request.GET.get(query_param)

    #         else:
    #             last_params = params_from_last_time(
    #                 request, key_prefix, query_params)
    #             if last_params and last_params != {}:
    #                 current_url = "%s?%s" % (request.META.get(
    #                     "PATH_INFO"), request.META.get("QUERY_STRING"))
    #                 new_url = update_url(current_url, last_params)
    #                 return HttpResponseRedirect(new_url)

    #         return view_func(*args, **kwargs)

    #     return decorator

    # return do_decorator
