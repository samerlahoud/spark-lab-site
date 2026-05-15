import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from xgboost import XGBClassifier
from scipy.stats import skew, kurtosis


# ── Constants ─────────────────────────────────────────────────────────────────
CP_LENGTH = 16
N_SUBCARRIERS = 64

# change to your  dataset path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "..", "data")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "output")

DEVICE_FILES = {
    "Legitimate 1":  "legitimate_device_01.npy",
    "Legitimate 2":  "legitimate_device_02.npy",
    "Legitimate 3":  "legitimate_device_03.npy",
    "Legitimate 4":  "legitimate_device_04.npy",
    "Attacker 1":    "attacker_device_05_impersonates_01.npy",
    "Attacker 2":    "attacker_device_06_impersonates_02.npy",
    "Attacker 3":    "attacker_device_07_impersonates_03.npy",
    "Attacker 4":    "attacker_device_08_impersonates_04.npy",
}


# ── Data Loading ──────────────────────────────────────────────────────────────
def load_dataset():
    iq_data_list, labels, device_names = [], [], []

    for i, (name, fname) in enumerate(DEVICE_FILES.items()):
        path = os.path.join(DATA_DIR, fname)
        data = np.load(path)  # (n_packets, 3840) complex64
        iq_data_list.append(data)
        labels.extend([i] * len(data))
        device_names.append(name)
        print(f"Loaded {name}: {data.shape}")

    iq_data = np.concatenate(iq_data_list, axis=0)
    labels = np.array(labels)

    print(f"\nTotal shape: {iq_data.shape}")
    print(f"Total labels: {labels.shape}")

    return iq_data, labels, device_names


# ── Feature Extraction ────────────────────────────────────────────────────────
def extract_features(iq_data):
    features_list = []

    for row in iq_data:
        real_part = np.array([c.real for c in row])
        imag_part = np.array([c.imag for c in row])
        complex_signal = real_part + 1j * imag_part

        mean_real = np.mean(real_part)
        mean_imag = np.mean(imag_part)
        std_real = np.std(real_part)
        std_imag = np.std(imag_part)
        skew_real = skew(real_part)
        skew_imag = skew(imag_part)
        kurt_real = kurtosis(real_part)
        kurt_imag = kurtosis(imag_part)

        fft_signal = np.fft.fft(complex_signal[CP_LENGTH:])
        magnitude_spectrum = np.abs(fft_signal[:N_SUBCARRIERS])
        phase_spectrum = np.angle(fft_signal[:N_SUBCARRIERS])

        spectral_mean = np.mean(magnitude_spectrum)
        spectral_std = np.std(magnitude_spectrum)
        spectral_flatness = (np.exp(np.mean(np.log(magnitude_spectrum + 1e-9)))
                             / (np.mean(magnitude_spectrum) + 1e-9))
        spectral_entropy = -np.sum(magnitude_spectrum * np.log(magnitude_spectrum + 1e-9))
        spectral_slope = np.polyfit(np.arange(len(magnitude_spectrum)), magnitude_spectrum, 1)[0]

        iq_imbalance = np.mean(real_part) / (np.mean(imag_part) + 1e-9)
        cfo_variance = np.var(np.angle(complex_signal[1:] * np.conj(complex_signal[:-1])))
        phase_noise_skewness = (np.mean((phase_spectrum - np.mean(phase_spectrum)) ** 3)
                                / (np.std(phase_spectrum) ** 3 + 1e-9))
        phase_noise_kurtosis = (np.mean((phase_spectrum - np.mean(phase_spectrum)) ** 4)
                                / (np.std(phase_spectrum) ** 4 + 1e-9))

        ideal_symbols = np.round(complex_signal.real) + 1j * np.round(complex_signal.imag)
        evm = np.sqrt(np.mean(np.abs(complex_signal - ideal_symbols) ** 2))

        autocorr_real = np.correlate(real_part, real_part, mode='full')[len(real_part) - 1]
        autocorr_imag = np.correlate(imag_part, imag_part, mode='full')[len(imag_part) - 1]
        energy_variation = np.var(np.abs(complex_signal))
        adaptive_modulation_std = np.std(np.real(fft_signal))
        sparsity = (np.sum(magnitude_spectrum < 0.1 * np.max(magnitude_spectrum))
                    / (len(magnitude_spectrum) + 1e-9))
        phase_diff = np.mean(np.diff(phase_spectrum))

        features_list.append([
            mean_real, mean_imag, std_real, std_imag,
            skew_real, skew_imag, kurt_real, kurt_imag,
            spectral_mean, spectral_std, spectral_flatness,
            spectral_entropy, spectral_slope,
            iq_imbalance, cfo_variance,
            phase_noise_skewness, phase_noise_kurtosis,
            evm, autocorr_real, autocorr_imag,
            energy_variation, adaptive_modulation_std,
            sparsity, phase_diff
        ])

    return np.array(features_list, dtype=np.float32)


# ── Classification & Visualization ───────────────────────────────────────────
def classify_and_plot(features, labels, device_names, test_size=0.2, random_state=42):
    X_train, X_test, y_train, y_test = train_test_split(
        features, labels, test_size=test_size, random_state=random_state, stratify=labels
    )

    clf = XGBClassifier(eval_metric='mlogloss', random_state=random_state)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, average='macro')
    rec = recall_score(y_test, y_pred, average='macro')
    f1 = f1_score(y_test, y_pred, average='macro')

    print(f"\n=== XGBoost Classification ===")
    print(f"Accuracy:  {acc:.4f}")
    print(f"Precision: {prec:.4f}")
    print(f"Recall:    {rec:.4f}")
    print(f"F1 Score:  {f1:.4f}")

    cm = confusion_matrix(y_test, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=device_names)

    fig, ax = plt.subplots(figsize=(10, 8))
    disp.plot(ax=ax, colorbar=True, xticks_rotation=45)
    ax.set_title("XGBoost Confusion Matrix — RF Device Fingerprinting")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "confusion_matrix.png"), dpi=300)
    plt.close()
    print("Saved: confusion_matrix.png")


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    iq_data, labels, device_names = load_dataset()
    features = extract_features(iq_data)
    print(f"Features shape: {features.shape}")

    classify_and_plot(features, labels, device_names)


if __name__ == "__main__":
    main()