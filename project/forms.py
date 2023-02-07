from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField(label='อีเมล์')
    password = forms.CharField(
        label ='รหัสผ่าน',
        widget=forms.PasswordInput(render_value=True)
    )

class SearchForm(forms.Form):
    name = forms.CharField(
        label='',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ป้อนชื่อ'})
)