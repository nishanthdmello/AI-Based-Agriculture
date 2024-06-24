// app/layout.js
import 'bootstrap/dist/css/bootstrap.min.css';
import './globals.css';

export const metadata = {
  title: 'Farming Feasibility Calculator',
  description: 'Calculate the feasibility of farming based on NPK values, soil moisture, and crop type.',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
