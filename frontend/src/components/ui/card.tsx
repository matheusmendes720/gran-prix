import * as React from 'react';
import { twMerge } from 'tailwind-merge';

// Create a simple className utility since we don't have @/lib/utils yet
const cn = (...classes: string[]) => twMerge(classes.join(' '));

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  children?: React.ReactNode;
}

const Card = React.forwardRef<HTMLDivElement, CardProps>(
  ({ className, children, ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={cn(
          "rounded-lg border bg-white p-6 shadow-sm",
          className
        )}
        {...props}
      >
        {children}
      </div>
    );
  }
);

Card.displayName = "Card";

export { Card };