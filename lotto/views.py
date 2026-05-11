import random
from django.shortcuts import render, redirect
from .models import LottoTicket, LottoRound

def index(request):
    tickets = LottoTicket.objects.all().order_by('-purchase_date')[:10]
    rounds = LottoRound.objects.all().order_by('-round_number')
    return render(request, 'lotto/index.html', {'tickets': tickets, 'rounds': rounds})

def buy_lotto(request):
    if request.method == "POST":
        nums = sorted(random.sample(range(1, 46), 6))
        nums_str = ",".join(map(str, nums))
        
        LottoTicket.objects.create(numbers=nums_str, is_automatic=True)
        return redirect('index')
    return render(request, 'lotto/buy.html')

def check_win(request):
    ticket_id = request.GET.get('ticket_id')
    round_num = request.GET.get('round_num')
    
    try:
        ticket = LottoTicket.objects.get(id=ticket_id)
        round_info = LottoRound.objects.get(round_number=int(round_num))
        
        my_nums = set(ticket.numbers.split(','))
        win_nums = set(round_info.win_numbers.split(','))
        match_count = len(my_nums & win_nums)
        
        prize = 0
        rank = 0
        if match_count == 6:
            prize = 2000000000
            rank = 1
        elif match_count == 5:
            prize = 50000000
            rank = 3
        elif match_count == 4:
            prize = 50000
            rank = 4
        elif match_count == 3:
            prize = 5000
            rank = 5

        return render(request, 'lotto/result.html', {
            'match_count': match_count,
            'ticket': ticket,
            'round': round_info,
            'prize': prize,
            'rank': rank
        })
    except Exception as e:
        return redirect('index')