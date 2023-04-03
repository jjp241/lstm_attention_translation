## Practical 3



Architektura Enkoder-Dekoder. Tylko zamiast warstwy feed-forward która jest w transformerach mamy LSTM:



## Pomysł 1: nieoptymalny

#### Po lewej:

LSTM w dwie strony - raz w prawo a raz w lewo i konkatenujemy wyniki potem (prostota!)

Do LSTM wchodzi indeks z word2vec

Na górze wychodzi z tego stack wszystkiego z lstm -> na górze mamy zaencodowany ciąg wektorów słowa z którego chcemy tłumaczyć.

Chcemy na podstawie tego w sposób autoregresywny.



#### Z Prawej:

Tutaj tylko z prawej do lewej LSTM - bo najpierw generujemy jedno słowo, potem kolejne (nie mamy informacji z prawej jeszcze co tam jest).



I teraz przechdozimy z tego ciągu na górze po lewej w kolejny ciąg na dole po prawej. **Ale mamy wąskie gardło wtedy!**



## Pomysł 2: z Attention

Po prawej: LSTM attentions - zestackowane na sobie

Tutaj dziwna atencja: zakładamy K = V, ale nie piszemy tego tak? **Multiplicative Attention** - działa podobnie jak zwykły attention (da się prztłumaczyć z jednej atencji na inną)



**Additive Attention** - konceptualnie inna rzecz. Dodajemy K i Q i patrzymy na ile te wektory się zneutralizują a na ile zamplifikują (mniejsza złożoność) ale tracimy możliwość porównania każdego wektora z każdym.





### BleuScore

Mamy kandydat i 3 inne referencyjne tłumaczenia zdania

c [-r1, -r2, -r3]

Liczymy sobie `ngram` -y (1-ngram, 2-ngram, 3-ngramy). Dla każdego `n-gramu` który występuje w słowie referencyjnym nalężącego ile razy on maksymalnie występował



candidate = `I love frogs and to be honest I love milk`

mamy ngram = `I love`

w `c` - 2

Patrzymy ile razy występował w referencyjnych tłumaczeniach:

```
-r1 0
-r2 1
-r3 0
```

maksymalnie w innych tłumaczeniach raz. Score: ile proporcjonalnie u nas względem u reszty i normalizujemy po sumie wszystkich ngramów. Trzeba jeszcze dodać