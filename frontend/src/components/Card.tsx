
import React from 'react';

interface CardProps {
  children: React.ReactNode;
  className?: string;
  onClick?: () => void;
}

const Card: React.FC<CardProps> = ({ children, className = '', onClick }) => {
  return (
    <div 
      onClick={onClick}
      className={`glass-card rounded-xl p-6 animate-subtle-glow ${className}`}
    >
      {children}
    </div>
  );
};

export default Card;