import torch
import torch.nn as nn
import json
from model import ShahajjoBrain

try:
    with open('data.txt', 'r', encoding='utf-8') as f:
        text = f.read()
except FileNotFoundError:
    print("❌ 'data.txt' পাওয়া যায়নি!")
    exit()

chars = sorted(list(set(text)))
vocab_size = len(chars)
stoi = {ch: i for i, ch in enumerate(chars)}
itos = {i: ch for i, ch in enumerate(chars)}

with open('vocab.json', 'w', encoding='utf-8') as f:
    json.dump({'stoi': stoi, 'itos': itos}, f, ensure_ascii=False)

encode = lambda s: [stoi[c] for c in s if c in stoi]
data = torch.tensor(encode(text), dtype=torch.long)

model = ShahajjoBrain(vocab_size)
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
criterion = nn.CrossEntropyLoss()

print("🚀 Shahajjo AI Training Started...")
model.train()

for epoch in range(300):
    inputs = data[:-1].unsqueeze(0)
    targets = data[1:].unsqueeze(0)

    optimizer.zero_grad()
    logits = model(inputs)
    loss = criterion(logits.view(-1, vocab_size), targets.view(-1))
    loss.backward()
    optimizer.step()

    if (epoch + 1) % 50 == 0:
        print(f"Epoch {epoch+1}/300 | Loss: {loss.item():.4f}")

torch.save(model.state_dict(), 'shahajjo_weights.pth')
print("✅ Training Complete! Saved 'shahajjo_weights.pth' and 'vocab.json'")
