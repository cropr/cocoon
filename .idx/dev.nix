# To learn more about how to use Nix to configure your environment
# see: https://developers.google.com/idx/guides/customize-idx-env
{ pkgs, ... }: {
  # Which nixpkgs channel to use.
  channel = "stable-24.05"; # or "unstable"

  # Use https://search.nixos.org/packages to find packages
  packages = [
    pkgs.python311
    pkgs.poetry
    pkgs.poethepoet
    pkgs.yarn
    pkgs.gtk3
  ];

  # Sets environment variables in the workspace
  env = {
    LD_LIBRARY_PATH = "${pkgs.stdenv.cc.cc.lib}/lib";
  };  
  idx = {
    # Search for the extensions you want on https://open-vsx.org/ and use "publisher.id"
    extensions = [
      # "vscodevim.vim"
      "ms-python.debugpy"
      "ms-python.python"
    ];

    # Enable previews
    previews = {
      enable = true;
      previews = {
        web = {
          # Example: run "npm run dev" with PORT set to IDX's defined port for previews,
          # and show it in IDX's web preview panel
          command = ["yarn" "run" "dev"];
          cwd = "frontend";
          manager = "web";
          env = {
            # Environment variables to set for your server
            PORT = "$PORT";
            API_URL = "8000-idx-cocoon-1739970435563.cluster-6yqpn75caneccvva7hjo4uejgk.cloudworkstations.dev";
          };
        };
      };
    };

    # Workspace lifecycle hooks
    workspace = {
      # Runs when a workspace is first created
      onCreate = {
        yarn-install = "cd frontend; yarn; cd ..";
      };
      # Runs when the workspace is (re)started
      onStart = {
        # Example: start a background task to watch and re-build backend code
        # watch-backend = "npm run watch-backend";
      };
    };
  };
  
}