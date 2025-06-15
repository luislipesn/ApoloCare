from django.shortcuts import redirect

def usuario_logado(view_func):
    def wrapper(request, *args, **kwargs):
        if 'id_usuario' not in request.session:
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper
