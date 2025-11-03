"""
Sistema de Retry e Recuperação de Erros
Implementa retry automático com backoff exponencial e recuperação inteligente
"""
import logging
import time
import random
from functools import wraps
from typing import Callable, Optional, List, Type, Tuple, Any
from pathlib import Path

logger = logging.getLogger(__name__)

class RetryHandler:
    """Handler para retry de operações com backoff exponencial"""
    
    def __init__(self,
                 max_retries: int = 3,
                 base_delay: float = 1.0,
                 max_delay: float = 60.0,
                 exponential_base: float = 2.0,
                 jitter: bool = True):
        """
        Args:
            max_retries: Número máximo de tentativas
            base_delay: Delay base em segundos
            max_delay: Delay máximo em segundos
            exponential_base: Base para backoff exponencial
            jitter: Adicionar jitter aleatório ao delay
        """
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.exponential_base = exponential_base
        self.jitter = jitter
    
    def retry(self,
              exceptions: Tuple[Type[Exception], ...] = (Exception,),
              on_failure: Optional[Callable] = None):
        """
        Decorator para retry de funções
        
        Args:
            exceptions: Tupla de exceções para capturar
            on_failure: Função chamada após cada falha (recebe tentativa e erro)
        """
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                last_exception = None
                
                for attempt in range(self.max_retries + 1):
                    try:
                        return func(*args, **kwargs)
                    except exceptions as e:
                        last_exception = e
                        
                        if attempt < self.max_retries:
                            # Calcular delay
                            delay = min(
                                self.base_delay * (self.exponential_base ** attempt),
                                self.max_delay
                            )
                            
                            # Adicionar jitter se habilitado
                            if self.jitter:
                                delay = delay * (0.5 + random.random() * 0.5)
                            
                            logger.warning(
                                f"Attempt {attempt + 1}/{self.max_retries + 1} failed for {func.__name__}: {e}"
                            )
                            logger.info(f"Retrying in {delay:.2f} seconds...")
                            
                            # Chamar callback de falha se fornecido
                            if on_failure:
                                on_failure(attempt + 1, e)
                            
                            time.sleep(delay)
                        else:
                            logger.error(
                                f"All {self.max_retries + 1} attempts failed for {func.__name__}"
                            )
                            raise
                
                raise last_exception
            
            return wrapper
        return decorator

def retry_with_recovery(func: Callable,
                       max_retries: int = 3,
                       recovery_strategies: Optional[List[Callable]] = None) -> Callable:
    """
    Decorator com estratégias de recuperação
    
    Args:
        func: Função a ser executada
        max_retries: Número máximo de tentativas
        recovery_strategies: Lista de funções de recuperação a tentar
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        handler = RetryHandler(max_retries=max_retries)
        
        # Tentar função original
        try:
            return handler.retry()(func)(*args, **kwargs)
        except Exception as e:
            logger.warning(f"Original function failed: {e}")
            
            # Tentar estratégias de recuperação
            if recovery_strategies:
                for i, recovery_func in enumerate(recovery_strategies):
                    try:
                        logger.info(f"Trying recovery strategy {i+1}/{len(recovery_strategies)}")
                        result = recovery_func(*args, **kwargs)
                        logger.info(f"Recovery strategy {i+1} succeeded")
                        return result
                    except Exception as recovery_error:
                        logger.warning(f"Recovery strategy {i+1} failed: {recovery_error}")
                        continue
            
            # Se todas as estratégias falharam, relançar exceção original
            raise
    
    return wrapper

class DownloadRetryHandler:
    """Handler especializado para downloads com recuperação"""
    
    def __init__(self, max_retries: int = 3):
        self.handler = RetryHandler(max_retries=max_retries, base_delay=2.0)
    
    def download_with_retry(self, download_func: Callable, *args, **kwargs):
        """Baixar com retry automático"""
        exceptions = (
            ConnectionError,
            TimeoutError,
            OSError,
            Exception  # Captura outras exceções de rede
        )
        
        return self.handler.retry(exceptions=exceptions)(download_func)(*args, **kwargs)

class FileOperationRetryHandler:
    """Handler para operações de arquivo com recuperação"""
    
    def __init__(self, max_retries: int = 3):
        self.handler = RetryHandler(max_retries=max_retries, base_delay=0.5)
    
    def read_with_retry(self, file_path: Path, read_func: Callable, *args, **kwargs):
        """Ler arquivo com retry"""
        exceptions = (IOError, PermissionError, FileNotFoundError)
        
        def read_wrapper():
            return read_func(file_path, *args, **kwargs)
        
        return self.handler.retry(exceptions=exceptions)(read_wrapper)
    
    def write_with_retry(self, file_path: Path, data: Any, write_func: Callable):
        """Escrever arquivo com retry"""
        exceptions = (IOError, PermissionError, OSError)
        
        def write_wrapper():
            # Garantir que diretório existe
            file_path.parent.mkdir(parents=True, exist_ok=True)
            return write_func(file_path, data)
        
        return self.handler.retry(exceptions=exceptions)(write_wrapper)

def create_backup_before_operation(file_path: Path):
    """Criar backup antes de operação destrutiva"""
    if file_path.exists():
        backup_path = file_path.with_suffix(file_path.suffix + '.backup')
        import shutil
        shutil.copy2(file_path, backup_path)
        logger.info(f"Created backup: {backup_path}")
        return backup_path
    return None

def restore_from_backup(file_path: Path):
    """Restaurar de backup"""
    backup_path = file_path.with_suffix(file_path.suffix + '.backup')
    if backup_path.exists():
        import shutil
        shutil.copy2(backup_path, file_path)
        logger.info(f"Restored from backup: {backup_path}")
        return True
    return False

