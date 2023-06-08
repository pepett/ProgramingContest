from django import forms

class Register(forms.Form):
    user_name = forms.CharField(label = "名前",widget=forms.TextInput(attrs={'placeholder':'スポティパイ太郎'}))
    user_mail = forms.EmailField(label = "メール",widget=forms.TextInput(attrs={'placeholder':'aaa@gmail.com'}))
    user_pass = forms.CharField(label = "パスワード",widget=forms.PasswordInput(attrs={'placeholder':'6字以上'}))
    user_image = forms.ImageField(label = "画像",)
    user_birthday = forms.DateTimeField(label = "誕生日",widget=forms.TextInput(attrs={'placeholder':'20002020'}))        
