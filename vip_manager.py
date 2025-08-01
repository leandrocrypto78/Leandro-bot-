import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class VIPManager:
    """VIP user management system"""
    
    def __init__(self):
        self.vip_users = {}  # user_id -> vip_data
        self.vip_packages = {
            'basic': {
                'price': 99,
                'duration': 30,
                'features': ['Real-time prices', 'Basic signals', 'Market news']
            },
            'premium': {
                'price': 299,
                'duration': 90,
                'features': ['All basic features', 'Premium signals', 'Chart analysis', 'Priority support']
            },
            'elite': {
                'price': 999,
                'duration': 365,
                'features': ['All premium features', 'Personal consultation', 'Exclusive opportunities', '24/7 support']
            }
        }
        logger.info("✅ VIP Manager initialized")
    
    def check_vip_status(self, user_id: int) -> bool:
        """Check if user has active VIP status"""
        try:
            if user_id in self.vip_users:
                vip_data = self.vip_users[user_id]
                expiry_date = vip_data.get('expiry_date')
                if expiry_date and datetime.now() < expiry_date:
                    return True
                else:
                    # Remove expired VIP
                    del self.vip_users[user_id]
            return False
        except Exception as e:
            logger.error(f"Error checking VIP status for user {user_id}: {e}")
            return False
    
    def get_vip_package_info(self, package_name: str) -> Optional[Dict]:
        """Get information about a VIP package"""
        return self.vip_packages.get(package_name)
    
    def get_all_packages(self) -> Dict:
        """Get all available VIP packages"""
        return self.vip_packages
    
    def add_vip_user(self, user_id: int, package_name: str, duration_days: int = None) -> bool:
        """Add or extend VIP access for a user"""
        try:
            package = self.vip_packages.get(package_name)
            if not package:
                return False
            
            if duration_days is None:
                duration_days = package['duration']
            
            expiry_date = datetime.now() + timedelta(days=duration_days)
            
            self.vip_users[user_id] = {
                'package': package_name,
                'expiry_date': expiry_date,
                'features': package['features']
            }
            
            logger.info(f"VIP access granted to user {user_id} for {package_name} package")
            return True
            
        except Exception as e:
            logger.error(f"Error adding VIP user {user_id}: {e}")
            return False
    
    def get_user_vip_info(self, user_id: int) -> Optional[Dict]:
        """Get VIP information for a specific user"""
        if self.check_vip_status(user_id):
            return self.vip_users.get(user_id)
        return None