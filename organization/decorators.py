from django.shortcuts import redirect

def user_has_organization(condition=True):   
    
    def method_wrapper(view_func):

        def decorator(request, *args, **kwargs):

            if request.user.info.has_organization() == condition:
                return view_func(request, *args, **kwargs)
            else:
                if request.user.info.has_organization() == False:
                    return redirect('org-none')
                else:
                    return redirect('org-dash')


        return decorator
    return method_wrapper
