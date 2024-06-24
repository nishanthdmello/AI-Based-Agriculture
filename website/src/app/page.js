// app/page.js
import Link from 'next/link';

export default function Home() {
  return (
    <div>
      <nav className="navbar navbar-expand-lg navbar-light bg-light">
        <div className="container-fluid">
          <Link className="navbar-brand" href="/">Farming Feasibility</Link>
          <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span className="navbar-toggler-icon"></span>
          </button>
          <div className="collapse navbar-collapse" id="navbarNav">
            <ul className="navbar-nav">
              <li className="nav-item">
                <Link className="nav-link active" aria-current="page" href="/">Home</Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link" href="/input">Calculator</Link>
              </li>
            </ul>
          </div>
        </div>
      </nav>
      <div className="container d-flex align-items-center justify-content-center" style={{ height: '80vh' }}>
        <div className="text-center">
          <h1>Welcome to the Farming Feasibility Calculator</h1>
          <p>Calculate the feasibility of farming based on NPK values, soil moisture, and crop type.</p>
          <Link href="/input" className="btn btn-primary">Get Started</Link>
        </div>
      </div>
    </div>
  );
}
