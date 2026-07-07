# Credentials and secrets handling

> Typ: policy | Doména: it | Citlivost: internal

# Credentials

# PTS NuGet registry

[NuGets](https://learn.microsoft.com/en-us/nuget/what-is-nuget) are .NET packages which are necessary to run our backend applications. If you need to run our application locally or even publish new packages, you will need to have access to the Package Registry, which is on our [GitLab](https://gitlab.praguelabs.com/pts/PTSframework/-/packages).

## How to get Username and Password for NuGet

1. You need to have access to [PTS](https://gitlab.praguelabs.com/groups/pts/-/group_members) group in GitLab. **Ask** @[Jan Pospíšil](mention://03113ef0-2fb8-451c-b343-70c04dd13ea8/user/77a5eb2b-e9fd-4c1d-b5fe-150a0a651212) **to give you access** if you don't already have it.

   
:::info
   For read only access to Registry, provide *Reporter* access. For pushing new packages, at least *Developer* access is needed. [Read more](https://gitlab.praguelabs.com/help/user/permissions) about role permissions.

   :::
2. Go to your Profile (user icon in the top right corner) > Preferences > [Access Tokens](https://gitlab.praguelabs.com/-/profile/personal_access_tokens) in GitLab.
3. Create a new Token with only `read_api` scope. In case you need to publish packages as well, choose `api` scope instead. *Make sure to remove Expiration date of the token!*\n\n[image omitted]
4. The generated Token is your Password. Username is your GitLab username - example: lukas.kmoch

:::warning
This Token basically works as a password to your GitLab account. It allows anyone with access to it to do anything you can do on GitLab.\n\n**Always store your Personal Access Tokens securely and do not share it with other users.** You are responsible for keeping it safe.

:::

## NuGet configuration

More info on how to configure NuGet in case you are setting up a new .NET project is documented elsewhere.
