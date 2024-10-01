import React from 'react';

const Card = ({ className, ...props }) => (
  <div className={`bg-white shadow-md rounded-lg ${className}`} {...props} />
);

const CardHeader = ({ className, ...props }) => (
  <div className={`px-6 py-4 border-b ${className}`} {...props} />
);

const CardTitle = ({ className, ...props }) => (
  <h3 className={`text-lg font-semibold ${className}`} {...props} />
);

const CardContent = ({ className, ...props }) => (
  <div className={`px-6 py-4 ${className}`} {...props} />
);

export { Card, CardHeader, CardTitle, CardContent };