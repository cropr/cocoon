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
    pkgs.hostname
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
          command = ["yarn" "dev" ];
          cwd = "frontend";
          manager = "web";
          env = {
            PORT = "$PORT";
            API_URL = "https://8000-idx-cocoon-1739970435563.cluster-6yqpn75caneccvva7hjo4uejgk.cloudworkstations.dev/";
          };
        };
      };
    };

    # Workspace lifecycle hooks
    workspace = {
      # Runs when a workspace is first created
      onCreate = {
        fe-build = "poe fe_build";
        be-build = "poe be_build";
      };
      # Runs when the workspace is (re)started
      onStart = {
        be-run = "poe be_run";
      };
    };
  };
  
}