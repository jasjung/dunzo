# Dunzo

https://pypi.org/project/dunzo/

## Installation

```shell  
pip install dunzo
```

## Upgrade 

```shell 
pip install --upgrade dunzo
```

## [sounds effect](https://mixkit.co/free-sound-effects/) 

- (Original name : name in this repo)  
- Uplifting flute notification : flute 
- Retro game notification : game  

## Usage 

In Python 

```py 
from dunzo import done 
done()
```

In Terminal:  

```sh 
done
```

However, to make the above work you have to follow a few steps. If you know how to bypass this, please tell me.  

```shell
# find your python path  
which python # it would look like the following 
#$ /Users/<your_user_name>/opt/anaconda3/bin/python

# If so, your done command will live here: '/Users/<your_user_name>/opt/anaconda3/bin/done'
# You want to add it in your zshrc or bash_profile to setup an alias.  
open .zshrc # or equivalent 
alias done='/Users/<your_user_name>/opt/anaconda3/bin/done'
source .zshrc

done # should output something like below:   
#$ Finished @ (Date) 2022-04-04 (Time) 06:18:59 PM PDT! Played flute sound
 
```

## Development 

```sh
# update your version 
poetry version <add_package_version> 
poetry publish --build
```

adding packages 

```shell
poetry add --dev <your package>
```

