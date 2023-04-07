## Practical 3 jp429585



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

\+ More flexible and effective - can capture more complex relations than dot product attention - because we can learn to extract specific information from both $h_i$ and $s_t$

\+ Works great in Encoder-Decoder models, where $h_i$ and $s_t$ have very different modalities and different scale

\- Highest computational cost - we have to feed forward both $h_i$ and $s_t$ 

\- Don't have ability to compare each vector to another one like in Multiplicative attention

\- More parameters to learn (more training data needed)



### 7 a)

First error I noted is the big number of `<unk>` tokens where big parts of translation should be. However i will describe this problem more in 7b) I will focus on linguistic problems:

- `it is a times sign` -> `to jest macierz razy znak` 

  Problem: `times sign` means in this example something different than `razy znak`, however it makes sense in most of the cases. More training data could fix that.

- `You could view this as the number 65 one time` -> `Możesz popatrzeć na to jako ilość 65 jednego czasu` 

  Again, `one time` can be somehow directly translated to `jednego czasu` however that is not the case here. 

- `That is going to approach 0.`  -> `To będzie 0` 

  Model missed a word `approach` - this may be caused by architecture and beam search, one advantage of NMT against other methods is that it allows to skip and add some words if needed. Probably word approach was underrepresented in data and had low score?

- `So in this video I'm just going to do a ton of examples.` -> `W tym filmie zrobię kilka przykładów` 

  "Kilka" means similar thing to "A ton", probably this phrase "A ton" was not common in dataset and "kilka" received bigger score. Including more data sources, not only scientific texts, would allow model to learn more common phrases like this one.

- `But let's say I have, I don't know, a 20 kelvin-- actually` -> `Ale powiedzmy, że mam 20 <unk>` 

  Here it is possible that model could finish that correctly but because `kelvin--` was not in target vocabulary it gave up and returned `<unk`> - I would suggest better tokenization in the NMT system, so when the word is not in the vocabulary we can split it into smaller tokens that exist in vocab.



### 7 b)

BLEU score: **5.58** 

Difference is huge because now our translated output is mostly `<unk>` and BLEU is very low then (for each translation there are no ngrams present in gold-standard translations - because there are only `<unk>`). This is result of bad coverage of vocabulary over text - very few words actually have their tokens in polish vocab.  Polish language have this issue because words in polish have many different cases, one noun, that in english have couple of forms (plural/singular/possesive) can have over 20 forms in Polish - that makes polish vocabulary significantly larger and hard to cover. 

I would suggest to perform tokenization in different way - instead of finding whole words in vocab, try to greedy take as much letters from word as possible in vocabulary. That way, words not covered by one token in vocab would still be covered by 2 or 3 tokens and not result in `<unk>` 





### 7 c)

##### Question 1:

```
Source Sentence s: So this means a strict subset.
Reference Translation r1 : Czyli to oznacza podzbiór wlaściwy.
Reference Translation r2 : W takim razie to oznacza podzbiór wlaściwy.
NMT Translation c1 : Czyli to podzbiór wlaściwy.
NMT Translation c2 : W takim razie to oznacza jest zbiór wlaściwy.
```

I wrote python code for that as well (stored in this repo)

For translation c1:

```
p1 = 1.0
p2 = 0.6666
c = 4
r* = 5
BP = 0.7788
BLEU = 0.635
```

for translation c2:

```
p1 = 0.75
p2 = 0.571
c = 8
r = 7
BP = 1
BLEU = 0.654
```

It loos like the second translation is better, however it just has words more common in reference translations but lacks grammatical sense, I don't agree with BLEU score. This is a huge drawback of BLEU score - it just counts ngrams and doesn't verify grammatical and semantical correctness.



##### Question 2:

```
Our hard drive was corrupted and we lost Reference Translation r2 . Please recompute BLEU
scores for c1 and c2 , this time with respect to r1 only. Which of the two NMT translations now receives the
higher BLEU score? Do you agree that it is the better translation?
```



For translation c1: **0.635**

For translation c2: **0.231** 

Now the first translation is better, which I can agree with, however this drastical change shows how sensitive BLEU is for reference translations.



##### Question 3:

```
Due to data availability, NMT systems are often evaluated with respect to only a single
reference translation. Please explain (in a few sentences) why this may be problematic.
```

This may be problematic, because there are often multiple correct translations - some may be even better than the reference one, and we still count other translations as bad. Also, we may overfit to training/test data when there is no room for some variance in the translation.



##### Question 4:

```
List two advantages and two disadvantages of BLEU, compared to human evaluation, as
an evaluation metric for Machine Translation.
```

Advantages of BLEU:

- Quick and efficient computation, can be done automatically
- Objectivity and no contradictions in giving scores, clearly defined rules

Disadvantages of BLEU:

- Doesn't rate grammar and semantic correctness, fluency or consistency in style. Very limited in what is actually in scope of BLEU score. Example of that is the second ($c_2$) translation in this task 

- Doesn't detect some huge, obvious errors in translation such that doesn't affect set of ngrams but completely change the meaning. Original sentence with one crucial word swapped give more BLEU score than whole sentence with the same meaning

  Example (both reference and translation in english for simplicity)

  ```
  Reference: I love going out with my friends on sundays
  Translation 1: I enjoy hanging out with colleagues on sundays BLEU: 0.37
  Translation 2: I hate going out with my friends on sundays BLEU: 0.81
  ```

  



