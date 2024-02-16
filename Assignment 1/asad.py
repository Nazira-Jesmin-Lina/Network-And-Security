# Importing necessary libraries
import torch  # PyTorch library for tensor computations
import torch.nn as nn  # Neural network module of PyTorch

# Function to convert context words to indices
def make_context_vector(context, word_to_ix):
    # List comprehension to get the indices of words in the context using the word_to_ix dictionary
    idxs = [word_to_ix[w] for w in context]
    # Convert the list of indices to a PyTorch tensor with data type long
    return torch.tensor(idxs, dtype=torch.long)

# Context size and embedding dimensionality constants
CONTEXT_SIZE = 2  # Context window size: 2 words to the left, 2 words to the right
EMBEDDING_DIM = 100  # Dimensionality of word embeddings

# Input text
raw_text = """
We are about to study the idea of a computational process.
Computational processes are abstract beings that inhabit computers.
As they evolve, processes manipulate other abstract things called data.
The evolution of a process is directed by a pattern of rules called a program.
People create programs to direct processes. In effect,
we conjure the spirits of the computer with our spells.
""".split()  # Splitting the text into a list of words

# Deduplicating the word list to create a vocabulary
vocab = set(raw_text)
# Size of the vocabulary
vocab_size = len(vocab)

# Creating word-to-index and index-to-word dictionaries
word_to_ix = {word: ix for ix, word in enumerate(vocab)}  # Mapping from word to index
ix_to_word = {ix: word for ix, word in enumerate(vocab)}  # Mapping from index to word

# Generating training data by creating context-target pairs
data = []
for i in range(2, len(raw_text) - 2):
    # Context consists of two words to the left and two words to the right of the target word
    context = [raw_text[i - 2], raw_text[i - 1], raw_text[i + 1], raw_text[i + 2]]
    target = raw_text[i]  # Target word is the current word in the iteration
    data.append((context, target))  # Append the context-target pair to the data list

# Definition of the Continuous Bag of Words (CBOW) model
class CBOW(nn.Module):
    def __init__(self, vocab_size, embedding_dim):
        super(CBOW, self).__init__()
        # Embedding layer: maps each word index to a dense vector representation
        self.embeddings = nn.Embedding(vocab_size, embedding_dim)
        # Linear layer 1: transforms the concatenated word embeddings to a hidden representation
        self.linear1 = nn.Linear(embedding_dim, 128)
        # Activation function 1: ReLU activation applied to the output of linear1
        self.activation_function1 = nn.ReLU()
        # Linear layer 2: transforms the hidden representation to a vector of vocab_size dimensionality
        self.linear2 = nn.Linear(128, vocab_size)
        # Activation function 2: LogSoftmax applied to the output of linear2
        self.activation_function2 = nn.LogSoftmax(dim=-1)

    # Forward pass through the model
    def forward(self, inputs):
        # Lookup word embeddings for the input word indices and sum them up
        embeds = sum(self.embeddings(inputs)).view(1, -1)
        # Pass the concatenated embeddings through linear1
        out = self.linear1(embeds)
        # Apply ReLU activation
        out = self.activation_function1(out)
        # Pass the output through linear2
        out = self.linear2(out)
        # Apply LogSoftmax activation
        out = self.activation_function2(out)
        return out

    # Function to get the embedding vector for a given word
    def get_word_embedding(self, word):
        # Convert the word to its corresponding index
        word_idx = torch.tensor([word_to_ix[word]])
        # Lookup the embedding for the word index and reshape it
        return self.embeddings(word_idx).view(1, -1)

# Instantiate the CBOW model
model = CBOW(vocab_size, EMBEDDING_DIM)

# Define the loss function (negative log likelihood loss)
loss_function = nn.NLLLoss()
# Define the optimizer (Stochastic Gradient Descent)
optimizer = torch.optim.SGD(model.parameters(), lr=0.001)

# Training the model
for epoch in range(50):
    total_loss = 0
    for context, target in data:
        # Convert the context words to indices
        context_vector = make_context_vector(context, word_to_ix)
        # Forward pass: compute log probabilities for the target word
        log_probs = model(context_vector)
        # Compute the loss based on the predicted probabilities and the actual target word index
        total_loss += loss_function(log_probs, torch.tensor([word_to_ix[target]]))
    # Zero gradients, perform a backward pass, and update the weights
    optimizer.zero_grad()
    total_loss.backward()
    optimizer.step()

# Testing the trained model
context = ['People', 'create', 'to', 'direct']
context_vector = make_context_vector(context, word_to_ix)
a = model(context_vector)

# Print the result
print(f'Raw text: {" ".join(raw_text)}\n')
print(f'Context: {context}\n')
print(f'Prediction: {ix_to_word[torch.argmax(a[0]).item()]}')
