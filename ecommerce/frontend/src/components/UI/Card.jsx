import React from 'react';

const Card = ({ children, className = '', hover = true, glass = false }) => {
  const baseClasses = 'rounded-xl shadow-lg transition-all duration-300';
  const hoverClasses = hover ? 'hover:shadow-xl hover:-translate-y-1' : '';
  const glassClasses = glass ? 'glass' : 'bg-white';

  return (
    <div className={`${baseClasses} ${hoverClasses} ${glassClasses} ${className}`}>
      {children}
    </div>
  );
};

export default Card;
