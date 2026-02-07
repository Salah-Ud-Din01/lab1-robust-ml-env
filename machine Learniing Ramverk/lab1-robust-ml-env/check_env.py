import torch
import sklearn
import pandas as pd

def main():
    print("=== Environment Check ===")

    # Kontrollera GPU
    if not torch.cuda.is_available():
        raise RuntimeError("GPU (CUDA) is required for this lab.")

    device = torch.device("cuda")
    print("Device:", device)
    print("GPU:", torch.cuda.get_device_name(0))

    # Versioner
    print("PyTorch version:", torch.__version__)
    print("Scikit-learn version:", sklearn.__version__)
    print("Pandas version:", pd.__version__)

    # Tensorberäkning på GPU
    x = torch.randn(1000, 1000, device=device)
    y = torch.randn(1000, 1000, device=device)
    z = x @ y

    print("Tensor computation successful on GPU")
    print("Result shape:", z.shape)

if __name__ == "__main__":
    main()
