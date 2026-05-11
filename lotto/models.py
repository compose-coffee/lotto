from django.db import models

class LottoRound(models.Model):
    round_number = models.IntegerField(unique=True) # 회차
    win_numbers = models.CharField(max_length=50)   # 당첨번호
    draw_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.round_number}회차 당첨번호"

class LottoTicket(models.Model):
    numbers = models.CharField(max_length=50)       # 선택한 번호들
    is_automatic = models.BooleanField(default=True) # 자동/수동 여부
    purchase_date = models.DateTimeField(auto_now_add=True)