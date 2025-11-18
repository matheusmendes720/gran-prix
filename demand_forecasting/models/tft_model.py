from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Optional

import numpy as np

try:  # pragma: no cover - optional dependency
    import torch
    from pytorch_lightning import LightningModule, Trainer
    from pytorch_lightning.callbacks import EarlyStopping
    from temporal_fusion_transformer_pytorch import TemporalFusionTransformer
    _HAS_TFT_LIB = True
except ModuleNotFoundError:  # pragma: no cover
    torch = None  # type: ignore
    LightningModule = object  # type: ignore
    Trainer = None  # type: ignore
    EarlyStopping = None  # type: ignore
    TemporalFusionTransformer = None  # type: ignore
    _HAS_TFT_LIB = False


logger = logging.getLogger(__name__)


@dataclass
class TFTConfig:
    max_epochs: int = 50
    gradient_clip_val: float = 0.1
    patience: int = 5
    batch_size: int = 256
    hidden_size: int = 64
    attention_heads: int = 4
    dropout: float = 0.1
    devices: Optional[int] = None  # defaults to all available GPUs


if _HAS_TFT_LIB:

    class TFTLightningModule(LightningModule):
        def __init__(self, model: TemporalFusionTransformer):
            super().__init__()
            self.model = model

        def forward(self, x):  # pragma: no cover - thin wrapper
            return self.model(x)

        def training_step(self, batch, batch_idx):  # pragma: no cover - heavy training
            y_hat = self.model(batch)
            loss = self.model.loss(batch, y_hat)
            self.log("train_loss", loss)
            return loss

        def validation_step(self, batch, batch_idx):  # pragma: no cover
            y_hat = self.model(batch)
            loss = self.model.loss(batch, y_hat)
            self.log("val_loss", loss, prog_bar=True)

        def configure_optimizers(self):  # pragma: no cover
            return torch.optim.Adam(self.parameters(), lr=1e-3)


    class TFTForecaster:
        def __init__(self, config: TFTConfig | None = None) -> None:
            self.config = config or TFTConfig()
            self.tft: Optional[TemporalFusionTransformer] = None
            self.trainer: Optional[Trainer] = None

        def _build_model(self, dataset) -> TemporalFusionTransformer:
            return TemporalFusionTransformer.from_dataset(
                dataset,
                hidden_size=self.config.hidden_size,
                attention_head_size=self.config.attention_heads,
                dropout=self.config.dropout,
            )

        def fit(self, dataset, validation):
            self.tft = self._build_model(dataset)
            lightning_module = TFTLightningModule(self.tft)
            devices = self.config.devices or torch.cuda.device_count()
            self.trainer = Trainer(
                max_epochs=self.config.max_epochs,
                gradient_clip_val=self.config.gradient_clip_val,
                accelerator="gpu" if torch.cuda.is_available() else "cpu",
                devices=devices,
                callbacks=[EarlyStopping(monitor="val_loss", patience=self.config.patience)],
                enable_checkpointing=False,
                logger=False,
            )
            self.trainer.fit(lightning_module, train_dataloaders=dataset, val_dataloaders=validation)

        def predict(self, dataloader) -> np.ndarray:
            if not self.trainer or not self.tft:
                raise RuntimeError("TFT model must be trained before inference")
            predictions = self.trainer.predict(self.tft, dataloaders=dataloader)
            return np.concatenate(predictions)

else:

    class TFTForecaster:
        def __init__(self, config: TFTConfig | None = None) -> None:  # pragma: no cover
            self.config = config or TFTConfig()
            logger.warning(
                "temporal_fusion_transformer_pytorch not installed; TFTForecaster is inactive."
            )

        def fit(self, *_, **__):  # pragma: no cover
            raise RuntimeError(
                "TFTForecaster requires temporal_fusion_transformer_pytorch. Install it to enable this model."
            )

        def predict(self, *_args, **_kwargs):  # pragma: no cover
            raise RuntimeError(
                "TFTForecaster requires temporal_fusion_transformer_pytorch. Install it to enable this model."
            )

