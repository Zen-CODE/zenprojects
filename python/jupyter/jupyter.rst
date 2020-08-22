Jupyter 
=======

To start on a public ip:

    jupyter notebook --ip=0.0.0.0

Terminal Settings
To set the font in the terminal:
```
terminal.term.setOption('fontFamily', 'Andale Mono');
terminal.term.setOption('theme', {
foreground:    '#9999ff',
background:    '#2d2d2d',
black:         '#646464',
brightBlack:   '#646464',
red:           '#f58e8e',
brightRed:     '#f58e8e',
green:         '#a9d3ab',
brightGreen:   '#a9d3ab',
yellow:        '#fed37e',
brightYellow:  '#fed37e',
blue:          '#7aabd4',
brightBlue:    '#7aabd4',
magenta:       '#d6add5',
brightMagenta: '#d6add5',
cyan:          '#79d4d5',
brightCyan:    '#79d4d5',
white:         '#d4d4d4',
brightWhite:   '#d4d4d4',
});
```

Launching a Slide Show
=======================

To launch a notebook as a slide show:

    jupyter nbconvert Command\ Line\ Computing.ipynb --to slides --post serve --port=1234

To define the slide:

    View -> Cell Toolbar -> Slideshow



