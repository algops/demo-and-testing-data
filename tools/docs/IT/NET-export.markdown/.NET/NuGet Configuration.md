# NuGet Configuration

# Commonly used public NuGet repos

Below is an example of commonly used NuGet repos. Your general `nuget.config` should be similar or the same as example on most projects.

**Path to nuget.config** `C:\Users\{USERNAME}\AppData\Roaming\NuGet\NuGet.Config`

```xml
<?xml version="1.0" encoding="utf-8"?>
<configuration>
    <packageSources>
        <add key="Microsoft Visual Studio Offline Packages" value="C:\Program Files (x86)\Microsoft SDKs\NuGetPackages\" />
        <add key="nuget.org" value="https://api.nuget.org/v3/index.json" />
        <add key="MyGet" value="https://www.myget.org/F/miniprofiler/api/v3/index.json" />
    </packageSources>
    <packageRestore>
        <add key="enabled" value="True" />
        <add key="automatic" value="True" />
    </packageRestore>
    <bindingRedirects>
        <add key="skip" value="False" />
    </bindingRedirects>
    <packageManagement>
        <add key="format" value="0" />
        <add key="disabled" value="False" />
    </packageManagement>  
</configuration>
```

# Private NuGet Repos

## GitLab repository

Run this command in CLI. You will need to [get your credentials first](./Credentials.md).

```bash
nuget source Add -Name "PTS GitLab" -Source "https://gitlab.iguana.tools/api/v4/groups/33/-/packages/nuget/index.json" -UserName <token_username> -Password <token>
```

or this **recommended** script variant

```bash
dotnet nuget Add source https://gitlab.iguana.tools/api/v4/groups/33/-/packages/nuget/index.json --name "PTS GitLab" --username <username> --password <password> 
```


#### Ubuntu users might find useful:

If you run the nuget add source and nothing shows up in the `$HOME/.nuget/Nuget/Nuget.config` try specifing the -ConfigFile param to this exact file