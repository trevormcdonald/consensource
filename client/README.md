# Client

## Prerequisites

  - Node8 `brew install node@8`
    -You will need to add `"/usr/local/opt/node@8/bin"` to your PATH

## Building

  - `npm install`
  - `npm run build`

## Running

From the project root, after building:

```
$ docker-compose -f docker-compose.yaml up
```

This will start an httpd server, with the files hosted available at
[http://localhost:8080](http://localhost:8080).

## Development

At development time, builds can run in watch mode.  This will compile changes at
file save time.  The output will provide source maps and will not be compressed.
It is recommended to test your work with a standard build, which outputs in
production mode.

This can be started by running:

```
$ npm run watch
```

### Linting

Code linting is provided through [ESLint](eslint.org) and is configured with the
`.eslint.js` file at the root of the `client` directory. It can be run via:

```
$ npm run lint
```

Formatting code can be done by running

```
$ npm run format
```

This will format the code using [es-beautifier](https://github.com/dai-shi/es-beautifier),
which is the same tool in the standard VSCode plugin, among others.

A non-zero return status means your code is linty.
