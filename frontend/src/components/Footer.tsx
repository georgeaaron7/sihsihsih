import React from 'react';
import { Github, Twitter, Mail } from 'lucide-react';

const Footer: React.FC = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-deep-900 border-t border-deep-700">
      <div className="max-w-7xl mx-auto px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand */}
          <div className="space-y-4">
            <div className="flex items-center gap-3">
              <img 
                src="/images/logo.png" 
                alt="WavOps Logo" 
                className="w-8 h-8 object-contain"
              />
              <span className="text-xl font-bold text-white">WavOps</span>
            </div>
            <p className="text-gray-400 text-sm">
              Interactive visualization of oceanographic data from Argo floats across the Indian Ocean.
            </p>
          </div>

          {/* Links */}
          <div>
            <h3 className="text-white font-semibold mb-4">Resources</h3>
            <ul className="space-y-2">
              <li>
                <a href="#" className="text-gray-400 hover:text-ocean-400 transition-colors text-sm">
                  Documentation
                </a>
              </li>
              <li>
                <a href="#" className="text-gray-400 hover:text-ocean-400 transition-colors text-sm">
                  API Reference
                </a>
              </li>
              <li>
                <a href="#" className="text-gray-400 hover:text-ocean-400 transition-colors text-sm">
                  Data Sources
                </a>
              </li>
            </ul>
          </div>

          {/* About */}
          <div>
            <h3 className="text-white font-semibold mb-4">About</h3>
            <ul className="space-y-2">
              <li>
                <a href="#" className="text-gray-400 hover:text-ocean-400 transition-colors text-sm">
                  Project Team
                </a>
              </li>
              <li>
                <a href="#" className="text-gray-400 hover:text-ocean-400 transition-colors text-sm">
                  Research
                </a>
              </li>
              <li>
                <a href="#" className="text-gray-400 hover:text-ocean-400 transition-colors text-sm">
                  Contact
                </a>
              </li>
            </ul>
          </div>

          {/* Social */}
          <div>
            <h3 className="text-white font-semibold mb-4">Connect</h3>
            <div className="flex space-x-4">
              <a
                href="#"
                className="text-gray-400 hover:text-ocean-400 transition-colors"
                aria-label="GitHub"
              >
                <Github className="w-5 h-5" />
              </a>
              <a
                href="#"
                className="text-gray-400 hover:text-ocean-400 transition-colors"
                aria-label="Twitter"
              >
                <Twitter className="w-5 h-5" />
              </a>
              <a
                href="#"
                className="text-gray-400 hover:text-ocean-400 transition-colors"
                aria-label="Email"
              >
                <Mail className="w-5 h-5" />
              </a>
            </div>
          </div>
        </div>

        {/* Bottom */}
        <div className="border-t border-deep-700 mt-8 pt-8 flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <p className="text-gray-400 text-sm">
            © {currentYear} Argo Float Dashboard. Built for oceanographic research.
          </p>
          <div className="flex items-center gap-2 text-gray-400 text-sm">
            <span>Made by Anuprabh, Manvitha, Aaron, Shreeya, Ashish and Disha.</span>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
