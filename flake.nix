{
  description = "tuya-convert: Flash alternative firmware on Tuya IoT devices";

  # Inputs: External dependencies for this flake
  inputs = {
    # Use nixos-unstable for latest packages
    # Can override with: nix develop --override-input nixpkgs github:NixOS/nixpkgs/nixos-24.05
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

    # Utility library for multi-system support
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils, ... }:
    # Generate outputs for all default systems (x86_64-linux, aarch64-linux, etc.)
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
          config.allowUnfree = true;
        };

        python = pkgs.python3;

        # Python environment with all required packages from requirements.txt
        pythonEnv = python.withPackages (ps: with ps; [
          # Standard packages available in nixpkgs
          paho-mqtt      # MQTT protocol client
          tornado        # Web server framework
          pycryptodomex  # Cryptographic library

          # sslpsk3: Custom package for SSL Pre-Shared Key support
          # This package is required for the PSK frontend server but not available in nixpkgs
          (ps.buildPythonPackage rec {
            pname = "sslpsk3";
            version = "1.0.0";

            # Use pyproject.toml-based build
            pyproject = true;
            format = "pyproject";

            # Fetch from PyPI
            src = pkgs.fetchPypi {
              inherit pname version;
              # Hash can be obtained by:
              # 1. Run: nix develop (will fail with wrong hash)
              # 2. Copy the "got: sha256-..." hash from error message
              # 3. Update this line with the correct hash
              # Or use: nix-prefetch-url --unpack https://files.pythonhosted.org/packages/.../sslpsk3-1.0.0.tar.gz
              hash = "sha256-BFScu9wtJy6eILMDzsGgLBlao3iQslGH1nEgQXZsBV4=";
            };

            # Build system requirements
            build-system = [ ps.setuptools ];

            # Native build inputs (available at build time)
            nativeBuildInputs = [ pkgs.openssl.dev ];

            # Build inputs (linked into the package)
            buildInputs = [ pkgs.openssl ];

            # Runtime dependencies
            propagatedBuildInputs = [ pkgs.openssl ];

            # Verify the package imports correctly
            pythonImportsCheck = [ "sslpsk3" ];

            meta = with pkgs.lib; {
              description = "Adds TLS-PSK (Transport Layer Security - Pre-Shared Key) support to Python 3.8+";
              homepage = "https://github.com/Ozon-ITMCMA/sslpsk3";
              license = licenses.asl20;
              maintainers = [ ];
            };
          })
        ]);

      in {
        # Development shell - activated with 'nix develop'
        devShells.default = pkgs.mkShell {
          name = "tuya-convert-dev";

          # All system dependencies required for tuya-convert
          buildInputs = [
            # Version control
            pkgs.git

            # Networking tools
            pkgs.iw          # Wireless configuration
            pkgs.dnsmasq     # DNS/DHCP server
            pkgs.hostapd     # Access point daemon
            pkgs.mosquitto   # MQTT broker
            pkgs.iproute2    # IP routing utilities
            pkgs.iputils     # Ping, etc.
            pkgs.nettools    # Network tools (ifconfig, netstat)

            # System utilities
            pkgs.util-linux  # System utilities
            pkgs.screen      # Terminal multiplexer
            pkgs.curl        # HTTP client
            pkgs.haveged     # Entropy daemon

            # Cryptography
            pkgs.openssl     # OpenSSL library and tools

            # Python environment with all packages
            pythonEnv
          ];

          shellHook = ''
            echo ""
            echo "╔════════════════════════════════════════════════════════════════╗"
            echo "║                    🔧 tuya-convert (Nix)                       ║"
            echo "╚════════════════════════════════════════════════════════════════╝"
            echo ""
            echo "✅ Development environment loaded successfully"
            echo ""
            echo "📦 Installed dependencies:"
            echo "   • Python ${python.version} with packages:"
            echo "     - paho-mqtt"
            echo "     - tornado"
            echo "     - pycryptodomex"
            echo "     - sslpsk3"
            echo "   • System tools: git, iw, dnsmasq, hostapd, mosquitto, screen"
            echo "   • Networking: iproute2, iputils, nettools"
            echo "   • Utilities: curl, haveged, openssl"
            echo ""
            echo "⚠️  IMPORTANT NOTES:"
            echo "   • This tool requires ROOT access to manage network interfaces"
            echo "   • NetworkManager and firewall must be stopped during flashing"
            echo "   • start_flash.sh handles service management automatically"
            echo ""
            echo "🚀 To flash a device:"
            echo "   ./start_flash.sh"
            echo ""
            echo "📚 Documentation:"
            echo "   • Quick Start: docs/Quick-Start-Guide.md"
            echo "   • Nix Guide:   docs/Using-Nix.md"
            echo "   • Troubleshooting: docs/Troubleshooting.md"
            echo ""
            echo "💡 Verify installation:"
            echo "   python3 --version"
            echo "   python3 -c 'import sslpsk3; print(f\"sslpsk3 {sslpsk3.__version__}\")'"
            echo ""
            echo "🔄 Exit this shell: type 'exit' or press Ctrl+D"
            echo ""
          '';

          # Environment variables
          TUYA_CONVERT_NIX = "1";  # Flag to indicate we're in Nix environment
        };

        # Optional: Package the application
        # Usage: nix run
        packages.default = pkgs.writeShellApplication {
          name = "tuya-convert";
          runtimeInputs = [ pythonEnv ] ++ (with pkgs; [
            git iw dnsmasq hostapd mosquitto iproute2 iputils
            nettools util-linux screen curl haveged openssl
          ]);
          text = ''
            cd ${self}
            exec ./start_flash.sh "$@"
          '';
        };

        # Apps for easy execution
        # Usage: nix run .#tuya-convert
        apps.default = {
          type = "app";
          program = "${self.packages.${system}.default}/bin/tuya-convert";
        };
      });
}
