from django.shortcuts import render
from django.http import HttpRequest
from .forms import Formulario
from .models import Operacion
from celery import Celery


# Create your views here.
class Operaciones(HttpRequest):
    def inicio(request):
        form = Formulario()
        return render(request, "nuevo.html", {"form": form})

    def guardar(request):
        try:
            form = Formulario(request.POST)
            if form.is_valid():
                app = Celery(
                    'task',
                    broker='amqp://user:bitnami@rabbitmq',
                    backend='rpc://user:bitnami@rabbitmq',
                )
                task1 = app.send_task('addTask', (request.POST['numero1'], request.POST['numero2'], request.POST['operador']))
                form.save()
                result = app.AsyncResult(task1)
                id = Operacion.objects.all().last().id
                app.send_task('updateTask', (result.get(), id,))

            return render(request, "nuevo.html", {"form": form, "mensaje": "ok"})
        except Exception as e:
            print(e)

    def listar(request):
        form = Operacion.objects.all()
        return render(request, "lista.html", {"form": form})