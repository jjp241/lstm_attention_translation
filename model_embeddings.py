"""Implementation based on https://github.com/pcyin/pytorch_nmt and 
Stanford CS224 2019 class.
"""
import torch.nn as nn


class ModelEmbeddings(nn.Module):
    """
    Class that converts input words to their embeddings.
    """

    def __init__(self, embed_size, vocab):
        """
        Init the Embedding layers.

        Args:
            embed_size (int): Embedding size (dimensionality)
            vocab (Vocab): Vocabulary object containing src and tgt languages
                See vocab.py for documentation.
        """
        super(ModelEmbeddings, self).__init__()
        self.embed_size = embed_size

        # default values
        self.source = None
        self.target = None

        src_pad_token_idx = vocab.src['<pad>']
        tgt_pad_token_idx = vocab.tgt['<pad>']

        # YOUR CODE HERE
        # TODO - Initialize the following variables:
        # self.source (Embedding Layer for source language)
        # self.target (Embedding Layer for target langauge)
        ###
        # Note:
        # 1. `vocab` object contains two vocabularies:
        # `vocab.src` for source
        # `vocab.tgt` for target
        # 2. You can get the length of a specific vocabulary by running:
        # `len(vocab.<specific_vocabulary>)`
        # 3. Remember to include the padding token for the specific vocabulary
        # when creating your Embedding.
        ###
        # Use the following docs to properly initialize these variables:
        # Embedding Layer:
        # https://pytorch.org/docs/stable/nn.html#torch.nn.Embedding
        
        source_lang_words = len(vocab.src)
        self.source = nn.Embedding(num_embeddings=source_lang_words,
                                   embedding_dim=self.embed_size,
                                   padding_idx=src_pad_token_idx)

        target_lang_words = len(vocab.tgt)
        self.target = nn.Embedding(num_embeddings=target_lang_words,
                                   embedding_dim=self.embed_size,
                                   padding_idx=tgt_pad_token_idx)

        # END YOUR CODE
