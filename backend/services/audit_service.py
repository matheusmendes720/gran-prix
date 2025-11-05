from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import json
from typing import Dict, Any, Optional
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AuditService:
    def __init__(self):
        # Use PostgreSQL database URL
        self.database_url = os.getenv(
            'DATABASE_URL', 
            'postgresql://nova_corrente:strong_password@localhost:5432/nova_corrente'
        )
        
        # Create engine
        self.engine = create_engine(self.database_url)
        self.SessionLocal = sessionmaker(bind=self.engine)
    
    def log_action(
        self, 
        actor: str, 
        action: str, 
        entity_type: Optional[str] = None, 
        entity_id: Optional[int] = None, 
        details: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ):
        """
        Log an action to the audit trail
        
        Args:
            actor: The user or system that performed the action
            action: The action that was performed
            entity_type: The type of entity affected (e.g., 'user', 'item', 'recommendation')
            entity_id: The ID of the specific entity affected
            details: Additional details about the action
            ip_address: The IP address of the actor
            user_agent: The user agent string
        """
        try:
            details_json = json.dumps(details or {})
            
            with self.SessionLocal() as session:
                session.execute(text("""
                    INSERT INTO support.audit_logs (actor, action, entity_type, entity_id, details, ip_address, user_agent, timestamp)
                    VALUES (:actor, :action, :entity_type, :entity_id, :details, :ip_address, :user_agent, NOW())
                """), {
                    'actor': actor,
                    'action': action,
                    'entity_type': entity_type,
                    'entity_id': entity_id,
                    'details': details_json,
                    'ip_address': ip_address,
                    'user_agent': user_agent
                })
                session.commit()
                
            logger.info(f"Audit log created: {actor} performed {action}")
            
        except Exception as e:
            logger.error(f"Failed to create audit log: {str(e)}")
            # Don't let audit logging failures break the main application flow
    
    def get_audit_logs(
        self, 
        actor: Optional[str] = None, 
        action: Optional[str] = None, 
        entity_type: Optional[str] = None, 
        entity_id: Optional[int] = None, 
        limit: int = 100,
        offset: int = 0
    ):
        """
        Retrieve audit logs with optional filters
        """
        try:
            base_query = "SELECT audit_id, actor, action, entity_type, entity_id, details, ip_address, user_agent, timestamp FROM support.audit_logs WHERE 1=1"
            params = {'limit': limit, 'offset': offset}
            
            if actor:
                base_query += " AND actor = :actor"
                params['actor'] = actor
            
            if action:
                base_query += " AND action = :action"
                params['action'] = action
                
            if entity_type:
                base_query += " AND entity_type = :entity_type"
                params['entity_type'] = entity_type
                
            if entity_id:
                base_query += " AND entity_id = :entity_id"
                params['entity_id'] = entity_id
                
            base_query += " ORDER BY timestamp DESC LIMIT :limit OFFSET :offset"
            
            with self.SessionLocal() as session:
                result = session.execute(text(base_query), params)
                logs = [dict(row._mapping) for row in result]
                
                # Get total count
                count_query = "SELECT COUNT(*) FROM support.audit_logs WHERE 1=1"
                count_params = {}
                
                if actor:
                    count_query += " AND actor = :actor"
                    count_params['actor'] = actor
                if action:
                    count_query += " AND action = :action"
                    count_params['action'] = action
                if entity_type:
                    count_query += " AND entity_type = :entity_type"
                    count_params['entity_type'] = entity_type
                if entity_id:
                    count_query += " AND entity_id = :entity_id"
                    count_params['entity_id'] = entity_id
                
                count_result = session.execute(text(count_query), count_params)
                total_count = count_result.scalar()
                
            return {
                'logs': logs,
                'total_count': total_count,
                'limit': limit,
                'offset': offset
            }
            
        except Exception as e:
            logger.error(f"Failed to retrieve audit logs: {str(e)}")
            return {'logs': [], 'total_count': 0, 'limit': limit, 'offset': offset}
    
    def cleanup_old_logs(self, days_to_keep: int = 90):
        """
        Remove audit logs older than specified number of days
        """
        try:
            with self.SessionLocal() as session:
                result = session.execute(text("""
                    DELETE FROM support.audit_logs 
                    WHERE timestamp < NOW() - INTERVAL ':days days'
                """), {'days': days_to_keep})
                session.commit()
                
            logger.info(f"Cleaned up audit logs older than {days_to_keep} days")
            return result.rowcount
            
        except Exception as e:
            logger.error(f"Failed to clean up audit logs: {str(e)}")
            return 0

# Create a global instance
audit_service = AuditService()