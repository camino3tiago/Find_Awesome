from .models import Profile
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.views import LoginView
from django.contrib import messages
from blog.models import Article
from .forms import UserCreationForm, ProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
import os
from config.settings import GRECAPTCHA_SECRETKEY, GRECAPTCHA_SITEKEY, DEFAULT_EMAIL_FROM


# def landing(request):
#     context = {}
#     return render(request, 
#         'mysite/landing.html',
#         context
#     )


def index(request):
    ranks = Article.objects.order_by('-like_count')[:2] # -をつけると降順（大⇨小）
    articles = Article.objects.all().order_by('-created_at')[:3]
    context = {
        'title': 'Travel Site',
        'articles': articles,
        'ranks': ranks,
    }
    return render(request,
        'mysite/index.html',
        context,
    )

class Login(LoginView):
    template_name = 'mysite/auth.html'

    # formにエラーがないか確認するためのメソッド（↓のsignup関数におけるform.is_valid():の部分に相応）
    def form_valid(self, form):
        messages.success(self.request, "You've successfully logged in!!")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'An error has occurred!!')
        return super().form_invalid(form)


def signup(request):
    context = {}
    if request.method == 'POST':
        form = UserCreationForm(request.POST)   # 送信されたrequestの内容をUserCreationFormに渡す
                                                # （ここでバリデーションやパスワードのハッシュ化）
        if form.is_valid():     # エラーがなければ、
            user = form.save(commit=False)  # DBにはまだ保存しない
            # user.is_active = False    # 例えば、is_activeをFalseにして、メール検証出来次第Trueにする。など
            user.save() # userを保存（おそらくDBにも？）

            # 自動でログインする
            login(request, user)

            messages.success(request, "You've successfully registered!!")     # 登録完了メッセージを表示
            return redirect('mysite:home')      # トップ画面にリダイレクト


    return render(request,
        'mysite/auth.html',
        context
    )


from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

class MyPageView(LoginRequiredMixin, View):
    context = {}

    def get(self, request):
        return render(request, 'mysite/mypage.html', self.context)
    
    def post(self, request):
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, 'Updated!!')
        return render(request, 'mysite/mypage.html', self.context)


class ContactView(View):
    context = {'grecaptcha_sitekey': GRECAPTCHA_SITEKEY}
    
    def get(self, request):
        return render(request, 
            'mysite/contact.html',
            self.context
        )

    def post(self, request):
        recaptcha_token = request.POST.get('g-recaptcha-response')
        res = grecaptcha_request(recaptcha_token)
        if not res:
            messages.error(request, 'failed with reCAPTCHA...')
            return render(request, 
                'mysite/contact.html',
                self.context
            )

        # ----- email設定 to me ----- # localhost:8000/contact/にGETで送信される
        from django.core.mail import send_mail
        subject = 'Inquiry'
        message = f'I received an inquiry. \n\
        名前：{request.POST.get("name")}\n\
        メールアドレス：{request.POST.get("email")}\n\
        内容：{request.POST.get("content")}\n以上'          # template(contact.html)のform内で指定したinputタグやらのname
        email_from = DEFAULT_EMAIL_FROM
        email_to = [    # 送信先は複数指定可
            DEFAULT_EMAIL_FROM,   
        ]
        send_mail(subject, message, email_from, email_to, )
        # ----- email設定 to me -----
        messages.success(request, 'Thank you for your inquiry!!')

        return render(request, 
            'mysite/contact.html',
            self.context
        )

def favorite(request):
    profile = Profile.objects.get(user=request.user)
    articles = Article.objects.filter(favorite=profile)
    print(profile, articles)
    context = {
        'profile': profile,
        'articles': articles,
    }
    return render(request, 
        'mysite/favorite.html',
        context
    )


def grecaptcha_request(token):
    from urllib import request, parse
    import json, ssl

    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)

    url = 'https://www.google.com/recaptcha/api/siteverify'
    headers = { 'content-type': 'application/x-www-form-urlencoded' }
    data = {
        'secret': GRECAPTCHA_SECRETKEY,
        'response': token,
    }
    data = parse.urlencode(data).encode()
    req = request.Request(
        url,
        method='POST',
        headers=headers,
        data=data,
    )
    f = request.urlopen(req, context=context)
    response = json.loads(f.read())
    f.close()
    return response['success']


def about(request):
    context = {}
    return render(request,
        'mysite/about.html',
        context
    )