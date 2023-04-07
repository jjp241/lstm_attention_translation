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



### 6 i)

Obtained BLEU score: **9.97**



### 6 j)

**Dot product attention**

\+ Computationally efficient, no need to multiply by whole weight matrix, just dot product of two vectors and optionally softmax

\- Not working if $s$ and $h$ have different scale(magnitude) - one becomes more important than other

\- Cannot learn scaling of attention weights. These two points make it not robust and very dependant on scale of input vectors. Can be still useful in self-attention where query, key and value comes from the same sequence.

**Multiplicative attention**

\+ Can capture complex relations between $h_i$ and $s_t$ than dot product attention by specifically extracting important things out of $h_i$ (by using $W$ feed-forward). 

\+ Allows scaling of attention weights (while dot-product cannot)

\- More expensive computationally than Dot product, but still less than Additive Attention

**Additive Attention**

\+ Most flexible and effective - can capture more complex relations than Multiplicative attention - because we can learn to extract specific information from both $h_i$ and $s_t$

\+ Works great in Encoder-Decoder models, where $h_i$ and $s_t$ have very different modalities and different scale

\- Highest computational cost - we have to feed forward both $h_i$ and $s_t$ 

\- More parameters to learn (more training data needed)



### 7 a)

