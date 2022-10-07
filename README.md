### Creating the Conda environment for this industry modelling project

Clone this project to your personal computer in a location of your choice.

At the command line, change the directory ('cd') to that selected location.
(So that the cloned project is the working directory.)

Now build the environment that this model operates within by executing:

```bash
$ conda env create --prefix ./env --file ./workflow/envs/environment.yml
```

Once the environment has been created, you can activate it with the following command:

```bash
$ source activate ./env
```

OR (depending on what command line program you're using):

```bash
$ conda activate ./env
```

Note that the `env` directory is *not* under version control as it can always be re-created from 
the `environment.yml` file as necessary.
(i.e. 'env/' is in the .gitignore file)
 
Also note: the environment should automatically activate (as long as you've created as per above) if you're working within VS Code and have chosen the cloned project directory as your working directory.
